import os
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configs.setting import SQLALCHEMY_DATABASE,SQLALCHEMY_DATABASE_URI

if not os.path.exists(SQLALCHEMY_DATABASE):
    os.makedirs(SQLALCHEMY_DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URI,echo=True)
#所有模型都继承这个基类
Base = declarative_base()

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_bases' #表名
    id = Column(Integer,primary_key=True,autoincrement=True,comment="知识库ID") #主键
    kb_name = Column(String(50),comment="知识库名称")
    kb_info = Column(String(200),comment="知识库简介(用于Agent)")

    def __repr__(self):
        return f"<KnowledgeBase(id='{self.id},kb_name='{self.kb_name}',kb_info='{self.kb_info})>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()