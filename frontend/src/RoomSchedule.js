import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment} from "semantic-ui-react";
import axios from "axios";

function RoomSchedule() {
    const [room, set_room] = useState("");
    const evs = []
    const data = {
        room_id: room
    }

    function getRoomSchedule() {
        if(evs.length !== 0) { // In case evs contain old data
            const len = evs.length
            for (let i = 0; i < len; i++) {
                evs.pop()
            }
        }
        axios.get('http://127.0.0.1:5000/coqui-bookings/Room/unavailable-time-rooms/' + data.room_id)
            .then(function (response) {
                console.log(response.data);
                let appointments = response.data;
                for (let i = 0; i < appointments.length; i++) {
                    evs.push({
                        'title': "Unavailable",
                        'allDay': false,
                        'start': new Date(appointments[i].unavailable_time_room_start),
                        'end': new Date(appointments[i].unavailable_time_room_finish)
                    })

                    // TODO DO ANOTHER AXIOS TO VERIFY IF BOOKING OR MARKED BY USER
                }
            }).catch(
            err => {
                console.log(err)
            })
    }
        const localizer = momentLocalizer(moment)
    return (
        <Segment>   <Grid columns={2} relaxed='very' stackable>
            <Grid.Column>
                <Form>
                    <Form.Input
                        id = 'room_id'
                        label='Room'
                        placeholder='Room Id'
                        onChange={(event) => {
                            set_room(event.target.value);
                        }}
                    />
                </Form>
            </Grid.Column>
            <Grid.Column>
                <Form>
                    <Button content='Get Schedule' style={{marginTop:28}} primary onClick={getRoomSchedule} />
                </Form>
            </Grid.Column>
        </Grid>
    <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={evs}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >
    </Calendar>
    </Container>
        </Segment>
    )

}
export default RoomSchedule;
