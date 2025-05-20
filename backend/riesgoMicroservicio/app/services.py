from backend.models import (
    db, SoftwareRisk, RiskOwnership, RiskClassification,
    RiskEvaluation, RiskControl, LikelihoodEnum, ImpactEnum, RiskMitigation
)

def register_software_risk(data):
    try:
        # Crear riesgo principal
        risk = SoftwareRisk(
            software_id=data["software_id"],
            risk_code=data["risk_code"],
            identified_at=data["identified_at"],
            title=data["title"],
            description=data.get("description", ""),
            causes=data.get("causes", ""),
            affects_critical_infrastructure=data.get("affects_critical_infrastructure", False),
            process=data.get("process", "")
        )
        db.session.add(risk)
        db.session.flush()  # Para obtener risk.id

        # Crear propiedad del riesgo
        ownership = data.get("ownership")
        if ownership:
            risk_owner = RiskOwnership(
                risk_id=risk.id,
                owner_name=ownership["owner_name"],
                owner_role=ownership["owner_role"]
            )
            db.session.add(risk_owner)
            db.session.flush()

        # Clasificación del riesgo
        classification = data.get("classification")
        if classification:
            risk_type = classification["risk_type"]

            # Determinar tipo de impacto según tipo de riesgo
            if risk_type in ["Fisico", "Logico", "Locativo"]:
                impact_type = "Continuidad Operativa"
            elif risk_type == "Legal":
                impact_type = "Legal"
            elif risk_type == "Reputacional":
                impact_type = "Imagen"
            else:
                impact_type = "Financiero" 
                
            risk_class = RiskClassification(
                risk_id=risk.id,
                risk_type=classification["risk_type"],
                confidentiality=classification["confidentiality"],
                integrity=classification["integrity"],
                availability=classification["availability"],
                impact_type=impact_type
            )
            db.session.add(risk_class)

        # Evaluación del riesgo
        evaluation = data.get("evaluation")
        if evaluation:
            likelihood_name = evaluation["likelihood"]
            impact_name = evaluation["impact"]
            likelihood = LikelihoodEnum[likelihood_name].value 
            impact = ImpactEnum[impact_name].value 
            valor_riesgo = likelihood * impact

            # Determinar zona de riesgo
            if valor_riesgo <= 3:
                risk_zone = "BAJA"
                acceptance = "Si"
            elif 4 <= valor_riesgo <= 6:
                risk_zone = "MODERADA"
                acceptance = "Si"
            elif 7 <= valor_riesgo <= 12:
                risk_zone = "ALTA"
                acceptance = "No"
            else:
                risk_zone = "EXTREMA"
                acceptance = "No"

            risk_eval = RiskEvaluation(
                risk_id=risk.id,
                likelihood=likelihood_name,
                impact=impact_name,
                risk_zone=risk_zone,
                acceptance=acceptance
            )
            db.session.add(risk_eval)
            db.session.flush()

        # Controles del riesgo
        controls = data.get("controls")
        if controls:
            control_type = controls["control_type"]

            def puntaje(valor, peso):
                return peso if valor == True else 0

            # Calcular calificación total
            control_rating = (
                puntaje(controls["has_mechanism"], 15) +
                puntaje(controls["has_manuals"], 15) +
                puntaje(controls["control_effective"], 30) +
                puntaje(controls["responsible_defined"], 15) +
                puntaje(controls["control_frequency_adequate"], 25)
            )

            # Determinar promedios según tipo
            preventive_controls_avg = control_rating if control_type == "PREVENTIVO" else 0
            corrective_controls_avg = control_rating if control_type == "CORRECTIVO" else 0

            # Función para cuadrantes
            def cuadrante(valor):
                if valor <= 50:
                    return 0
                elif 51 <= valor <= 75:
                    return 1
                elif 76 <= valor <= 100:
                    return 2
                else:
                    return 2  # > 100

            reduce_likelihood_quadrants = cuadrante(preventive_controls_avg)
            reduce_impact_quadrants = cuadrante(corrective_controls_avg)

            control = RiskControl(
                risk_id=risk.id,
                control_type=control_type,
                has_mechanism=controls["has_mechanism"],
                has_manuals=controls["has_manuals"],
                control_effective=controls["control_effective"],
                responsible_defined=controls["responsible_defined"],
                control_frequency_adequate=controls["control_frequency_adequate"],
                control_rating=control_rating,
                preventive_controls_avg=preventive_controls_avg,
                reduce_likelihood_quadrants=reduce_likelihood_quadrants,
                corrective_controls_avg=corrective_controls_avg,
                reduce_impact_quadrants=reduce_impact_quadrants
            )
            db.session.add(control)

            mitigation = RiskMitigation(
                risk_id=risk.id,
                evaluation_id=risk_eval.id if evaluation else None,
                ownership_id=risk_owner.id if ownership else None,
                risk_code=risk.risk_code,
                risk_zone=risk_zone,
                risk_description=risk.description,
                responsible=risk_owner.owner_name if ownership else "No asignado",
                phase=None,
                response_type=None,
                mitigation_plan=None
            )
            db.session.add(mitigation)

        db.session.commit()
        return {"message": "Riesgo registrado correctamente", "risk_id": risk.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
