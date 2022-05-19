import streamlit as st

st.set_page_config(
     page_title="Sortable Repeating Panel"
)

with open("styles/style.css") as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

events = ['Dinner Party', 'Birthday Party', 'Marriage', 'PhD Party', 'Party Party', 'Oktoberfest', 'Christmas Party', 'Carnival']
# ----------------------------------------------------------------------------------------------------------------------
st.markdown('### Sort events by Dates')

if 'events_sortable_by_date' not in st.session_state:
    st.session_state['events_sortable_by_date'] = st.multiselect("events sortable by date", events)
else:
    last_list = st.session_state['events_sortable_by_date']
    st.session_state['events_sortable_by_date'] = st.multiselect("events sortable by date", events, default=st.session_state['events_sortable_by_date'])
    if last_list != st.session_state['events_sortable_by_date']:
        st.experimental_rerun()

if len(st.session_state['events_sortable_by_date']) > 0:
    list_of_events_sorted_by_date = []
    for item in st.session_state['events_sortable_by_date']:
        container_sortable_by_date = st.container()
        col1_sorted_by_date, col2_sorted_by_date, col3_sorted_by_date = container_sortable_by_date.columns(3)
        with col1_sorted_by_date:
            st.write(item)
        with col2_sorted_by_date:
            event_date = st.date_input('Date', key=f'{item}_date')
        with col3_sorted_by_date:
            number_of_guests = st.number_input('Number of Guests', min_value=0, max_value=100, step=1, key=item)

        single_event = {
                        'event': item,
                        'date': event_date,
                        'number of guests': number_of_guests
                        }
        list_of_events_sorted_by_date.append(single_event)

    sort_events = st.button('Sort by Date')
    if sort_events:
        list_of_events_sorted_by_date.sort(key=lambda complication_item: complication_item['date'])
        interim_event_list_sorted_by_dates = []
        for item in list_of_events_sorted_by_date:
            interim_event_list_sorted_by_dates.append(item['event'])
        st.session_state['events_sortable_by_date'] = interim_event_list_sorted_by_dates
        st.experimental_rerun()

# ----------------------------------------------------------------------------------------------------------------------
st.markdown('### Sort Events by Pressing Up/Down-Buttons')

if 'events_sortable_by_buttons' not in st.session_state:
    st.session_state['events_sortable_by_buttons'] = st.multiselect("events sortable by buttons", events)
else:
    last_list = st.session_state['events_sortable_by_buttons']
    st.session_state['events_sortable_by_buttons'] = st.multiselect("events sortable by buttons", events, default=st.session_state['events_sortable_by_buttons'])
    if last_list != st.session_state['events_sortable_by_buttons']:
        st.experimental_rerun()


def sort_by_buttons(event_list: list):
    list_of_events_sortable_by_buttons = []
    if len(event_list) > 0:
        for index_2, item_2 in enumerate(event_list):
            container_sortable_by_buttons = st.container()
            col1_sortable_by_buttons, col2_sortable_by_buttons, col3_sortable_by_buttons, col4_sortable_by_buttons = container_sortable_by_buttons.columns(4)
            with col1_sortable_by_buttons:
                st.write(item_2)
            with col2_sortable_by_buttons:
                number_of_guests_2 = st.number_input('Number of Guests', min_value=0, max_value=100, step=1, key=f'{item_2}_button')
            with col3_sortable_by_buttons:
                if index_2 > 0:
                    move_up = st.button('up', key=f'{item_2}_button_up')
                    if move_up:
                        list_of_events_sortable_by_buttons[index_2 - 1]['order index'] += 1
                        index_2 -= 1
            with col4_sortable_by_buttons:
                if index_2 < len(event_list) - 1:
                    move_down = st.button('down', key=f'{item_2}_button_down')
                    if move_down:
                        index_2 += 1

            single_event_sortable_by_buttons = {
                            'event': item_2,
                            'order index': index_2,
                            'number of guests': number_of_guests_2
                            }
            list_of_events_sortable_by_buttons.append(single_event_sortable_by_buttons)

        # the order index of the list element below (press move_down) has to be changed outside the loop
        for list_index, list_item in enumerate(list_of_events_sortable_by_buttons):
            if list_index > 0:
                if list_item['order index'] == list_of_events_sortable_by_buttons[list_index - 1]['order index']:
                    list_item['order index'] -= 1

    return list_of_events_sortable_by_buttons


if len(st.session_state['events_sortable_by_buttons']) > 0:
    event_order = sort_by_buttons(st.session_state['events_sortable_by_buttons'])
    interim_complication_list_sortable_by_buttons = [{} for i in enumerate(event_order)]
    for index, item in enumerate(event_order):
        interim_complication_list_sortable_by_buttons[item['order index']] = item['event']
    # Important: only rerun the script if the order changed -> no infinite loop!
    if interim_complication_list_sortable_by_buttons != st.session_state['events_sortable_by_buttons']:
        st.session_state['events_sortable_by_buttons'] = interim_complication_list_sortable_by_buttons
        st.experimental_rerun()
