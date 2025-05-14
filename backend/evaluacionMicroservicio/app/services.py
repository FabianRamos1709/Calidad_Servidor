from backend.models import db, Evaluation, EvaluationDetail, EvaluationCharacteristicSummary, Subcharacteristic, Software
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
from sqlalchemy.orm import joinedload

def create_evaluation(data):
    try:
        software_id = data.get('software_id')
        details = data.get('details', [])

        if not software_id or not details:
            return None, 'Campos Incompletos'

        evaluation = Evaluation(
            software_id=software_id,
        )
        db.session.add(evaluation)
        db.session.flush()  

        grouped = defaultdict(lambda: {
            'sub_scores': [],
            'percentage': 0.0
        })

        for detail in details:
            sub_id = detail.get('subcharacteristic_id')
            score = detail.get('score')
            comment = detail.get('comment', '')
            char_id = detail.get('characteristic_id')
            char_percent = detail.get('characteristic_percentage')

            evaluation_detail = EvaluationDetail(
                evaluation_id=evaluation.id,
                subcharacteristic_id=sub_id,
                score=score,
                comment=comment
            )
            db.session.add(evaluation_detail)

            grouped[char_id]['sub_scores'].append(score)
            grouped[char_id]['percentage'] = char_percent

        global_score = 0.0
        for char_id, info in grouped.items():
            scores = info['sub_scores']
            percentage = info['percentage']
            value = sum(scores)
            max_value = len(scores) * 3
            result_percentage = (value / max_value) * 100 if max_value > 0 else 0.0
            weighted_percentage = (result_percentage * percentage) / 100

            global_score += weighted_percentage

            summary = EvaluationCharacteristicSummary(
                evaluation_id=evaluation.id,
                characteristic_id=char_id,
                value=value,
                max_value=max_value,
                result_percentage=round(result_percentage, 2),
                weighted_percentage=round(weighted_percentage, 2)
            )
            db.session.add(summary)

        evaluation.global_score_percentage = round(global_score, 2)
        db.session.commit()

        return evaluation, None
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, str(e)

def get_evaluation_details_by_software_id(software_id):
    evaluation = Evaluation.query.filter_by(software_id=software_id).order_by(Evaluation.date.desc()).first()
    if not evaluation:
        return None

    details = EvaluationDetail.query.filter_by(evaluation_id=evaluation.id).options(
        joinedload(EvaluationDetail.subcharacteristic).joinedload(Subcharacteristic.characteristic)
    ).all()

    grouped = {}
    for detail in details:
        sub = detail.subcharacteristic
        qc = sub.characteristic

        if qc.name not in grouped:
            grouped[qc.name] = {
                'quality_characteristic_id': qc.id,
                'quality_characteristic_name': qc.name,
                'subcharacteristics': []
            }

        grouped[qc.name]['subcharacteristics'].append({
            'subcharacteristic_id': sub.id,
            'subcharacteristic_name': sub.name,
            'score': detail.score,
            'comment': detail.comment
        })

    result = list(grouped.values())

    return {
        'evaluation_id': evaluation.id,
        'characteristics': result
    }

def get_result_label(percentage):
    if percentage <= 30:
        return "Deficiente"
    elif percentage <= 50:
        return "Insuficiente"
    elif percentage <= 70:
        return "Aceptable"
    elif percentage <= 81:
        return "Sobresaliente"
    else:
        return "Excelente"

def get_evaluated_softwares_by_user(user_id):
    softwares = Software.query.filter_by(user_id=user_id).options(
        joinedload(Software.evaluations)
    ).all()

    results = []
    for software in softwares:
        if not software.evaluations:
            continue

        latest_evaluation = max(software.evaluations, key=lambda e: e.date)
        percentage = float(latest_evaluation.global_score_percentage or 0)
        result_label = get_result_label(percentage)

        results.append({
            'software_id': software.id,
            'software_name': software.name,
            'evaluation_id': latest_evaluation.id,
            'evaluation_date': latest_evaluation.date.strftime('%d/%m/%Y'),
            'global_percentage': f"{percentage:.2f}%",
            'result': result_label
        })

    return results

def get_characteristic_summary_by_software(software_id, evaluation_id):
    evaluation = Evaluation.query.filter_by(id=evaluation_id, software_id=software_id).first()

    if not evaluation:
        return []

    summaries = EvaluationCharacteristicSummary.query.filter_by(evaluation_id=evaluation.id).options(
        joinedload(EvaluationCharacteristicSummary.characteristic)
    ).all()

    result = []
    for summary in summaries:
        result.append({
            'characteristic_name': summary.characteristic.name,
            'value': summary.value,
            'max_value': summary.max_value,
            'result_percentage': f"{summary.result_percentage:.2f}%",
            'weighted_percentage': f"{summary.weighted_percentage:.2f}%",
            'max_possible_percentage': f"{summary.characteristic.weight_percentage:.2f}%"
        })

    return {
        'evaluation_id': evaluation.id,
        'software_id': software_id,
        'summaries': result
    }
