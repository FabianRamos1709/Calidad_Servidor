from app.models import db, Software, SoftwareParticipant

def create_software(name, city, general_objective, description, version):
    existing_software = Software.query.filter_by(name= name).first()
    if existing_software:
        return None

    new_software = Software(name= name, city = city, general_objective = general_objective, description = description, version = version)

    db.session.add(new_software)
    db.session.commit()
    return new_software

def create_participant(name, role):
    existing_participant = SoftwareParticipant.query.filter_by(name= name).first()
    if existing_participant:
        return None

    new_participant = SoftwareParticipant(name= name, role = role)

    db.session.add(new_participant)
    db.session.commit()
    return new_participant