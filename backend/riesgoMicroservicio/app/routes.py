from flask import Blueprint, request, jsonify
from app.services import register_software_risk
from backend.models import SoftwareRisk, RiskEvaluation, Software, db, LikelihoodEnum, ImpactEnum
from sqlalchemy.orm import joinedload

riesgo_routes = Blueprint('risk', __name__)

@riesgo_routes.route('/registrar', methods=['POST'])
def register_risk():
    data = request.get_json()
    result, status = register_software_risk(data)
    return jsonify(result), status
@riesgo_routes.route('/evaluaciones/<int:user_id>', methods=['GET'])
def listar_evaluaciones_riesgo(user_id):
    try:
        # Consulta más simple y segura
        riesgos = (
            db.session.query(SoftwareRisk, Software, RiskEvaluation)
            .join(Software, SoftwareRisk.software_id == Software.id)
            .join(RiskEvaluation, SoftwareRisk.id == RiskEvaluation.risk_id)
            .filter(Software.user_id == user_id)
            .all()
        )

        print(f"Riesgos encontrados: {len(riesgos)}")

        data = []
        for riesgo_tuple in riesgos:
            try:
                riesgo, software, evaluation = riesgo_tuple
                
                # Manejar los enums correctamente
                likelihood_value = 1  # valor por defecto
                impact_value = 1      # valor por defecto
                
                # Debug: ver qué tipo de dato tenemos
                print(f"Likelihood type: {type(evaluation.likelihood)}, value: {evaluation.likelihood}")
                print(f"Impact type: {type(evaluation.impact)}, value: {evaluation.impact}")
                
                # Procesar likelihood
                if evaluation.likelihood:
                    if hasattr(evaluation.likelihood, 'value'):
                        # Es un enum object
                        likelihood_value = evaluation.likelihood.value
                    elif isinstance(evaluation.likelihood, str):
                        # Es un string, convertir a enum
                        try:
                            likelihood_enum = LikelihoodEnum[evaluation.likelihood]
                            likelihood_value = likelihood_enum.value
                        except KeyError:
                            print(f"Likelihood enum no encontrado: {evaluation.likelihood}")
                            likelihood_value = 1
                    else:
                        # Asumir que es un valor numérico directo
                        likelihood_value = int(evaluation.likelihood)
                
                # Procesar impact
                if evaluation.impact:
                    if hasattr(evaluation.impact, 'value'):
                        # Es un enum object
                        impact_value = evaluation.impact.value
                    elif isinstance(evaluation.impact, str):
                        # Es un string, convertir a enum
                        try:
                            impact_enum = ImpactEnum[evaluation.impact]
                            impact_value = impact_enum.value
                        except KeyError:
                            print(f"Impact enum no encontrado: {evaluation.impact}")
                            impact_value = 1
                    else:
                        # Asumir que es un valor numérico directo
                        impact_value = int(evaluation.impact)

                valor_riesgo = likelihood_value * impact_value

                # Formatear la fecha de manera segura
                evaluation_date = "N/A"
                if riesgo.identified_at:
                    evaluation_date = riesgo.identified_at.strftime("%Y-%m-%d")

                data.append({
                    "risk_id": riesgo.id,
                    "software_id": riesgo.software_id,
                    "software_name": software.name,
                    "risk_code": riesgo.risk_code or "N/A",
                    "zona_riesgo": evaluation.risk_zone or "N/A",
                    "valor_riesgo": valor_riesgo,
                    "evaluation_date": evaluation_date,
                    "acceptance": evaluation.acceptance or "N/A",
                })

                print(f"Procesado riesgo {riesgo.id}: likelihood={likelihood_value}, impact={impact_value}, valor={valor_riesgo}")

            except Exception as item_error:
                print(f"Error procesando riesgo: {str(item_error)}")
                import traceback
                print(f"Error detalle: {traceback.format_exc()}")
                continue

        print(f"Data final: {len(data)} riesgos procesados")
        return jsonify(data), 200

    except Exception as e:
        print(f"Error en listar_evaluaciones_riesgo: {str(e)}")
        import traceback
        print(f"Traceback completo: {traceback.format_exc()}")
        
        # Intentar una consulta más básica para debug
        try:
            basic_count = db.session.query(SoftwareRisk).join(Software).filter(Software.user_id == user_id).count()
            print(f"Riesgos básicos encontrados para user {user_id}: {basic_count}")
        except Exception as debug_e:
            print(f"Error en consulta básica: {debug_e}")
        
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500
    

@riesgo_routes.route('/detalle/<int:risk_id>', methods=['GET'])
def obtener_detalle_riesgo(risk_id):
    try:
        from backend.models import SoftwareRisk, db

        riesgo = SoftwareRisk.query.get(risk_id)

        if not riesgo:
            return jsonify({"error": "Riesgo no encontrado"}), 404

        data = {
            "risk_id": riesgo.id,
            "software_id": riesgo.software_id,
            "risk_code": riesgo.risk_code,
            "title": riesgo.title,
            "description": riesgo.description,
            "causes": riesgo.causes,
            "process": riesgo.process,
            "identified_at": riesgo.identified_at.strftime('%Y-%m-%d'),
            "affects_critical_infrastructure": riesgo.affects_critical_infrastructure,
            "owner": {
                "name": riesgo.ownership.owner_name if riesgo.ownership else "N/A",
                "role": riesgo.ownership.owner_role if riesgo.ownership else "N/A"
            },
            "classification": {
                "risk_type": str(riesgo.classification.risk_type.value) if riesgo.classification else "N/A",
                "confidentiality": riesgo.classification.confidentiality if riesgo.classification else False,
                "integrity": riesgo.classification.integrity if riesgo.classification else False,
                "availability": riesgo.classification.availability if riesgo.classification else False,
                "impact_type": riesgo.classification.impact_type if riesgo.classification else "N/A"
            },
            "evaluation": {
                "likelihood": str(riesgo.evaluation.likelihood.name) if riesgo.evaluation else "N/A",
                "impact": str(riesgo.evaluation.impact.name) if riesgo.evaluation else "N/A",
                "risk_zone": riesgo.evaluation.risk_zone if riesgo.evaluation else "N/A",
                "acceptance": riesgo.evaluation.acceptance if riesgo.evaluation else "N/A"
            },
            "controls": {
                "control_type": riesgo.controls.control_type if riesgo.controls else "N/A",
                "rating": str(riesgo.controls.control_rating) if riesgo.controls else "0",
                "has_mechanism": riesgo.controls.has_mechanism if riesgo.controls else False,
                "has_manuals": riesgo.controls.has_manuals if riesgo.controls else False,
                "control_effective": riesgo.controls.control_effective if riesgo.controls else False,
                "responsible_defined": riesgo.controls.responsible_defined if riesgo.controls else False,
                "control_frequency_adequate": riesgo.controls.control_frequency_adequate if riesgo.controls else False
            }
        }

        return jsonify(data), 200

    except Exception as e:
        print("Error al obtener detalle de riesgo:", str(e))
        return jsonify({"error": str(e)}), 500
