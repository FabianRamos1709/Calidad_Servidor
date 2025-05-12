from app.models import db, QualityCharacteristic, Subcharacteristic

def create_characteristic_with_subs(name, description, weight_percentage, subcharacteristics):

    new_char = QualityCharacteristic(
        name=name,
        description=description,
        weight_percentage=weight_percentage
    )
    db.session.add(new_char)
    db.session.flush()  

    for sub in subcharacteristics:
        sub_name = sub.get('name')
        sub_desc = sub.get('description', '')

        if not sub_name:
            continue
        existing = Subcharacteristic.query.filter_by(name=sub_name).first()
        if existing:
            continue

        new_sub = Subcharacteristic(
            name=sub_name,
            description=sub_desc,
            characteristic_id=new_char.id
        )
        db.session.add(new_sub)
    db.session.commit()
    return new_char

def get_all_characteristics():
    characteristics = QualityCharacteristic.query.all()
    results = []

    for char in characteristics:
        sub_count = Subcharacteristic.query.filter_by(characteristic_id=char.id).count()
        results.append({
            'id': char.id,
            'name': char.name,
            'description': char.description,
            'weight_percentage': float(char.weight_percentage),
            'subcharacteristic_count': sub_count
        })

    return results


def get_characteristic_with_subs(char_id):
    characteristic = QualityCharacteristic.query.get(char_id)
    if not characteristic:
        return None

    subs = Subcharacteristic.query.filter_by(characteristic_id=char_id).all()

    return {
        'id': characteristic.id,
        'name': characteristic.name,
        'description': characteristic.description,
        'weight_percentage': float(characteristic.weight_percentage),
        'subcharacteristics': [
            {
                'id': sub.id,
                'name': sub.name,
                'description': sub.description,
                'max_score': sub.max_score
            } for sub in subs
        ]
    }

def update_characteristic_with_subs(char_id, name, description, weight_percentage, subcharacteristics):
    characteristic = QualityCharacteristic.query.get(char_id)
    if not characteristic:
        return None

    characteristic.name = name
    characteristic.description = description
    characteristic.weight_percentage = weight_percentage

    for sub in subcharacteristics:
        sub_id = sub.get('id')
        sub_name = sub.get('name')
        sub_desc = sub.get('description', '')

        if sub_id:
            existing = Subcharacteristic.query.get(sub_id)
            if existing and existing.characteristic_id == char_id:
                existing.name = sub_name
                existing.description = sub_desc
        else:
            new_sub = Subcharacteristic(
                name=sub_name,
                description=sub_desc,
                characteristic_id=char_id
            )
            db.session.add(new_sub)

    db.session.commit()
    return characteristic

def delete_characteristic(char_id):
    characteristic = QualityCharacteristic.query.get(char_id)
    if not characteristic:
        return False
    db.session.delete(characteristic)
    db.session.commit()
    return True

def delete_subcharacteristic(sub_id):
    sub = Subcharacteristic.query.get(sub_id)
    if not sub:
        return False
    db.session.delete(sub)
    db.session.commit()
    return True