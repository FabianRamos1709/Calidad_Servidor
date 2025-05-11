from app.models import db, QualityCharacteristic, Subcharacteristic

def create_characteristic(name, description, weight_percentage):
    existing_characteristic = QualityCharacteristic.query.filter_by(name= name).first()
    if existing_characteristic:
        return None

    new_characteristic = QualityCharacteristic(name= name, description = description, weight_percentage = weight_percentage)

    db.session.add(new_characteristic)
    db.session.commit()
    return new_characteristic

def get_all_characteristics():
    return QualityCharacteristic.query.all()

def get_characteristic_by_id(char_id):
    return QualityCharacteristic.query.get(char_id)

def update_characteristic(char_id, name=None, description=None, weight_percentage=None):
    characteristic = QualityCharacteristic.query.get(char_id)
    if not characteristic:
        return None
    if name:
        characteristic.name = name
    if description:
        characteristic.description = description
    if weight_percentage is not None:
        characteristic.weight_percentage = weight_percentage
    db.session.commit()
    return characteristic

def delete_characteristic(char_id):
    characteristic = QualityCharacteristic.query.get(char_id)
    if not characteristic:
        return False
    db.session.delete(characteristic)
    db.session.commit()
    return True


def create_subcharacteristic(name, description):
    existing_participant = Subcharacteristic.query.filter_by(name= name).first()
    if existing_participant:
        return None

    new_subcharactetristic = Subcharacteristic(name= name, description = description)

    db.session.add(new_subcharactetristic)
    db.session.commit()
    return new_subcharactetristic

def get_subcharacteristics_by_characteristic(char_id):
    return Subcharacteristic.query.filter_by(characteristic_id=char_id).all()

def get_subcharacteristic_by_id(sub_id):
    return Subcharacteristic.query.get(sub_id)

def update_subcharacteristic(sub_id, name=None, description=None, max_score=None):
    sub = Subcharacteristic.query.get(sub_id)
    if not sub:
        return None
    if name:
        sub.name = name
    if description:
        sub.description = description
    if max_score is not None:
        sub.max_score = max_score
    db.session.commit()
    return sub

def delete_subcharacteristic(sub_id):
    sub = Subcharacteristic.query.get(sub_id)
    if not sub:
        return False
    db.session.delete(sub)
    db.session.commit()
    return True