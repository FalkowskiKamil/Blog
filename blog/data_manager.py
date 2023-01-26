from blog.models import Entry, db

class DataManager:
    def __init__(self, db):
        self._db = db

    def get_all_posts(self, published=True):
        return Entry.query.filter_by(is_published=published).order_by(Entry.pub_date.desc())
    
    def add_post(self, title, body, is_published):
        entry = Entry(
            title=title,
            body=body,
            is_published=is_published
            )
        db.session.add(entry)
        db.session.commit()

    def delete_post(self, entry_id):   
        draft_to_delete=data_manager.get_post(entry_id)
        db.session.delete(draft_to_delete)
        db.session.commit()

    def get_draft(self, published=False):
        return Entry.query.filter_by(is_published=published).order_by(Entry.pub_date.desc())

    def get_post(self, entry_id=id):
	    return Entry.query.filter_by(id=entry_id).first_or_404()
    
data_manager = DataManager(db)