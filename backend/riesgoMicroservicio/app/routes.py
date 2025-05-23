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
def detalle_riesgo(risk_id):
    try:
        risk = SoftwareRisk.query.get_or_404(risk_id)
        software = Software.query.get_or_404(risk.software_id)

        response = {
            "software": {
                "id": software.id,
                "name": software.name,
                "version": software.version,
            },
            "risk": {
                "id": risk.id,
                "risk_code": risk.risk_code,
                "title": risk.title,
                "identified_at": risk.identified_at.strftime("%Y-%m-%d"),
                "description": risk.description,
                "causes": risk.causes,
                "affects_critical_infrastructure": risk.affects_critical_infrastructure,
                "process": risk.process
            },
            "classification": {
                "risk_type": risk.classification.risk_type.value if risk.classification else None,
                "confidentiality": risk.classification.confidentiality,
                "integrity": risk.classification.integrity,
                "availability": risk.classification.availability,
                "impact_type": risk.classification.impact_type
            } if risk.classification else {},
            "evaluation": {
                "likelihood": risk.evaluation.likelihood.name,
                "impact": risk.evaluation.impact.name,
                "risk_zone": risk.evaluation.risk_zone,
                "acceptance": risk.evaluation.acceptance,
                "valor_riesgo": LikelihoodEnum[risk.evaluation.likelihood.name].value * ImpactEnum[risk.evaluation.impact.name].value
            } if risk.evaluation else {},
            "controls": {
                "control_type": risk.controls.control_type,
                "has_mechanism": risk.controls.has_mechanism,
                "has_manuals": risk.controls.has_manuals,
                "control_effective": risk.controls.control_effective,
                "responsible_defined": risk.controls.responsible_defined,
                "control_frequency_adequate": risk.controls.control_frequency_adequate,
                "control_rating": float(risk.controls.control_rating),
                "reduce_likelihood_quadrants": risk.controls.reduce_likelihood_quadrants,
                "reduce_impact_quadrants": risk.controls.reduce_impact_quadrants,
            } if risk.controls else {},
            "mitigation": {
                "responsible": risk.mitigations[0].responsible if risk.mitigations else "No asignado",
                "risk_zone": risk.mitigations[0].risk_zone if risk.mitigations else None
            }
        }

        return jsonify(response), 200

    except Exception as e:
        print("Error en detalle_riesgo:", str(e))
        return jsonify({"error": "Error al obtener detalle del riesgo"}), 500
