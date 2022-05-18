import streamlit as st


st.set_page_config(
     page_title="Sortable Reapeating Panel"
)

with open("styles/style.css") as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

if 'events' not in st.session_state:
    st.session_state['events'] = st.multiselect("Events",
                                                ['Dinner Party', 'Birthday Party', 'Marriage',
                                                 'PhD Party', 'Party Party'])
else:
    last_list = st.session_state['events']
    st.session_state['events'] = st.multiselect("Events", ['Dinner Party', 'Birthday Party', 'Marriage',
                                                 'PhD Party', 'Party Party'], default=st.session_state['events'])
    if last_list != st.session_state['events']:
        st.experimental_rerun()


if len(st.session_state['events']) > 0:
    list_of_events = []
    for item in st.session_state['events']:
        container_complications = st.container()
        col1, col2, col3 = container_complications.columns(3)
        with col1:
            st.write(item)
        with col2:
            event_date = st.date_input('Date', key=item)
        with col3:
            number_of_guests = st.number_input('Number of Guests', min_value=0, max_value=100,step=1, key=item)

        single_event = {
                        'event': item,
                        'date': event_date,
                        'number of guests': number_of_guests
                        }
        list_of_events.append(single_event)

    sort_events = st.button('Sort by Date')
    if sort_events:
        list_of_events.sort(key=lambda complication_item: complication_item['date'])
        interim_event_list_sorted_by_dates = []
        for item in list_of_events:
            interim_event_list_sorted_by_dates.append(item['event'])
        st.session_state['events'] = interim_event_list_sorted_by_dates
        st.experimental_rerun()

