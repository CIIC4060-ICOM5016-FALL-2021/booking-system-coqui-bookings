import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment} from "semantic-ui-react";
import axios from "axios";

function UserSchedule() {
    const evs = []
    const data = {
        user_id: localStorage.getItem("user_id")
    }
        axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/unavailable-time-users/' + data.user_id)
            .then(function (response) {
                console.log(response.data);
                let appointments = response.data;
                for (let i = 0; i < appointments.length; i++) {
                    evs.push({
                        'title': "Unavailable",
                        'allDay': false,
                        'start':new Date(appointments[i].unavailable_time_user_start),
                        'end': new Date(appointments[i].unavailable_time_user_finish)
                    })

                    // TODO DO ANOTHER AXIOS TO VERIFY IF BOOKING OR MARKED BY USER
                }
            }).catch(
                err => {
                    console.log("Error:" + err)
                })

    const localizer = momentLocalizer(moment)

    return <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={evs}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >
    </Calendar>
    </Container>

}
export default UserSchedule;
