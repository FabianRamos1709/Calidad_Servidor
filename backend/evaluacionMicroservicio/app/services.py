from backend.models import db, Evaluation, EvaluationDetail, EvaluationCharacteristicSummary
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict

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
