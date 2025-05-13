from backend.models import db, Software, SoftwareParticipant

def create_software_with_participants(name, city, general_objective, description, version, participants, user_id):
    existing_software = Software.query.filter_by(name=name).first()
    if existing_software:
        return {'success': False, 'message': 'El software ya existe'}

    new_software = Software(
        name=name,
        city=city,
        general_objective=general_objective,
        description=description,
        version=version,
        user_id=user_id
    )
    db.session.add(new_software)
    db.session.flush()  

    for p in participants:
        existing_participant = SoftwareParticipant.query.filter_by(name=p.get('name')).first()
        if existing_participant:
            continue  

        new_participant = SoftwareParticipant(
            name=p.get('name'),
            role=p.get('role'),
            software_id=new_software.id
        )
        db.session.add(new_participant)

    db.session.commit()
    return {'success': True}
