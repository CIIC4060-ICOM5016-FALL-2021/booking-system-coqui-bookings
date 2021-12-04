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

    const getUserId = event => {
        const data = {
            user_email: localStorage.getItem("user_email")
        }
        Axios.post("https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/login", data).then(
            res => {
                return res.data[1]
            }).catch(
            err => {
                console.log("Error:" + err)
            })
    }
    const getUserSchedule = event => {
        const user_id = getUserId()
        Axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/' + user_id +'/schedule')
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
