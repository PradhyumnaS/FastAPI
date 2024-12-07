import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main():
    st.title("Todo List App with Streamlit")

    db = next(get_db())

    with st.form("add_todo_form", clear_on_submit=True):
        title = st.text_input("Add a new Todo:")
        submitted = st.form_submit_button("Add Todo")
        if submitted and title.strip():
            new_todo = models.Todo(title=title.strip())
            db.add(new_todo)
            db.commit()
            st.rerun() 

    todos = db.query(models.Todo).all()

    if todos:
        st.subheader("Todo List")
        for todo in todos:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"{'✅' if todo.complete else '⬜'} {todo.title}")
            if col2.button("Toggle Complete", key=f"toggle_{todo.id}"):
                todo.complete = not todo.complete
                db.commit()
                st.rerun()  
            if col3.button("Delete", key=f"delete_{todo.id}"):
                db.delete(todo)
                db.commit()
                st.rerun()  
    else:
        st.info("No todos yet. Add one above!")

if __name__ == "__main__":
    main()
