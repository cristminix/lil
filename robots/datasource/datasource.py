from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from robots.datasource.models import Base,Config,User,App,Course,Section,Toc,StreamLocation,Transcript,DMSetup,DMStatus,AccountSetting 
from robots.datasource.models import MConfig, MCourse,MExerciseFile,MSection,MToc,MPrx,MStreamLocation,MTranscript,MAuthor

class DataSource:
    mConfig=None
    def __init__(self, path):
        # Replace 'sqlite:///your_database_name.db' with the actual path to your database file
        self.engine = create_engine('sqlite:///%s' % (path))
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.conn=self.session.connection()
        
        self.m_config = MConfig(self.session)
        self.m_course = MCourse(self)
        self.m_section = MSection(self)
        self.m_exercise_file = MExerciseFile(self)
        self.m_toc = MToc(self)
        self.m_prx = MPrx(self)
        self.m_stream_location = MStreamLocation(self)
        self.m_transcript = MTranscript(self)
        self.m_author = MAuthor(self)
