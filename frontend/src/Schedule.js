import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import Axios from "axios";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){
    const data = {
        user_id: localStorage.getItem("user_id")
    }
    const getUserSchedule = event => {
        Axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/' + data.user_id +'/schedule')
            .then( res => {
                console.log(res.data)
            }
    ).catch (err => {
            return "NOT FOUND ERROR";
        })
 }
    const [dates, setDates] = useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now())
    }]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)

    return <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>
        <Button
            fluid
            onClick={getUserSchedule}
        >Load Schedule </Button>
    </Container>


}
export default Schedule;
