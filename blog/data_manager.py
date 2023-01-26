from blog.models import Entry, db

class DataManager:
    def __init__(self, db):
        self._db = db

    def get_all_posts(self, published=True):
        return Entry.query.filter_by(is_published=published).order_by(Entry.pub_date.desc())
    
    def get_post(self, entry_id=id):
	    return Entry.query.filter_by(id=entry_id).first_or_404()
    
data_manager = DataManager(db)