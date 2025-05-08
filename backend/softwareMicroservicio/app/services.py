from app.models import db, Software

def create_software(name, city, general_objective, description, version):
    existing_software = Software.query.filter_by(name= name).first()
    if existing_software:
        return None

    new_software = Software(name= name, city = city, general_objective = general_objective,description = description, version = version)

    db.session.add(new_software)
    db.session.commit()
    return new_software