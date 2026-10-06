from db_server.base import KnowledgeBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

def add_kb_to_db(session:Session,kb_name:str,kb_info:str):
    try:
        kb = session.query(KnowledgeBase).filter(KnowledgeBase.kb_name.ilike(kb_name)).first()
        if not kb:
            kb = KnowledgeBase(kb_name=kb_name,kb_info=kb_info)
            session.add(kb)
            session.commit()
            print(f"KnowledgeBase'{kb_name}'create successfully.")
        else:
            kb.kb_info = kb_info
            session.commit()
            print(f"KnowledgeBase'{kb_name}'updated successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError:{e}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred:{e}")

def del_kb_from_db(session: Session, kb_name: str):
    try:
        # 查询是否存在指定名称的知识库
        kb_to_delete = session.query(KnowledgeBase).filter_by(kb_name=kb_name).first()

        if kb_to_delete:
            # 如果存在，删除知识库
            session.delete(kb_to_delete)
            session.commit()
            print(f"KnowledgeBase '{kb_name}' deleted successfully.")
        else:
            print(f"KnowledgeBase '{kb_name}' does not exist.")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

def list_kb_from_db(session: Session):
    all_kbs = session.query(KnowledgeBase).all()
    # 将结果转换为列表
    kbs_list = [
        {
            # "id": kb.id,
            "kb_name": kb.kb_name,
            "kb_info": kb.kb_info
        }
        for kb in all_kbs
    ]
    return kbs_list
