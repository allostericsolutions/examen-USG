import streamlit as st
import random

def mostrar_contacto_empresa():
    # Mostrar la imagen de la empresa con tamaño ajustado
    st.image("https://i.imgur.com/LzPcPIk.png", caption='Allosteric Solutions', width=350)

    # Compartir la página empresarial y el correo
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[Visita nuestra página web](https://www.allostericsolutions.com)")
    with col2:
        st.markdown("Contacto: [franciscocuriel@allostericsolutions.com](mailto:franciscocuriel@allostericsolutions.com)")

# List of organs
peritoneal_organs = [
    "Stomach", "Liver", "Spleen", "First part of the Duodenum", "Jejunum",
    "Ileum", "Transverse Colon", "Sigmoid Colon", "Appendix", "Upper Rectum"
]
retroperitoneal_organs = [
    "Kidneys", "Adrenal Glands", "Ureters", "Pancreas (except tail)",
    "Duodenum (except first part)", "Ascending Colon", "Descending Colon",
    "Middle and Lower Rectum", "Abdominal Aorta", "Inferior Vena Cava"
]

# Combine and shuffle the lists
all_organs = peritoneal_organs + retroperitoneal_organs
random.shuffle(all_organs)

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'answered_questions' not in st.session_state:
    st.session_state['answered_questions'] = []
if 'incorrect_answers' not in st.session_state:
    st.session_state['incorrect_answers'] = []
if 'all_organs' not in st.session_state:
    st.session_state['all_organs'] = all_organs.copy()  # Use a copy to avoid shuffling the global list


def check_answer(organ, response):
    if (organ in peritoneal_organs and response == "Peritoneal") or \
            (organ in retroperitoneal_organs and response == "Retroperitoneal"):
        st.session_state['score'] += 1
    else:
        st.session_state['incorrect_answers'].append(organ)

    st.session_state['answered_questions'].append(organ)
    st.session_state['all_organs'].remove(organ)


# Main function to render the quiz
def render_quiz():
    # Mostrar información de contacto arriba
    mostrar_contacto_empresa()

    st.title("Organ Classification Quiz")

    if len(st.session_state['all_organs']) == 0:
        st.write("No more organs to classify.")
    else:
        organ = st.session_state['all_organs'][0]

        st.subheader(f"Classify: {organ}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Peritoneal", key=f"{organ}_peritoneal"):
                check_answer(organ, "Peritoneal")
                st.experimental_rerun()
        with col2:
            if st.button("Retroperitoneal", key=f"{organ}_retroperitoneal"):
                check_answer(organ, "Retroperitoneal")
                st.experimental_rerun()

    if st.button("Show Grade"):
        show_grade()

    # Mostrar información de contacto abajo
    mostrar_contacto_empresa()

def show_grade():
    total_questions = len(peritoneal_organs + retroperitoneal_organs)
    score = st.session_state['score']
    percentage = (score / total_questions) * 100

    st.write(f"Your final grade is: {score}/{total_questions} ({percentage:.1f}%)")

    if percentage <= 50:
        st.write("You need a lot of work, keep going!")
    elif percentage <= 70:
        st.write("The effort has been good, but there is still more to do.")
    elif percentage <= 85:
        st.write("Good, but you can do more.")
    elif percentage <= 90:
        st.write("Very good!")
    else:
        st.write("Excellent!")

    # Reset for another round
    st.session_state['score'] = 0
    st.session_state['answered_questions'] = []
    st.session_state['incorrect_answers'] = []
    st.session_state['all_organs'] = all_organs.copy()
    random.shuffle(st.session_state['all_organs'])


if __name__ == "__main__":
    render_quiz()
