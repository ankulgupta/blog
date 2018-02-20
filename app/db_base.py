

def init_db():
	import models
	Base.metadata.create_all(engine)