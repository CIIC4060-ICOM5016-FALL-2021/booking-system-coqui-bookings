import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment} from "semantic-ui-react";
import Axios from "axios";

function RoomSchedule() {
    const [room, set_room] = useState("");
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [mark_open, setMarkOpen] = useState(false);
    const localizer = momentLocalizer(moment);
    const [booking_name, set_booking_name] = useState("");
    const [booking_start_date, set_booking_start_date] = useState("");
    const [booking_start_time, set_booking_start_time] = useState("");
    const [booking_finish_date, set_booking_finish_date] = useState("");
    const [booking_finish_time, set_booking_finish_time] = useState("");
    const [booking_invitee_id, set_booking_invitee_id] = useState("");
    const [room_id, set_room_id] = useState("");

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
        Axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/Room/unavailable-time-rooms/' + data.room_id)
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

    const handleMarkClick = () =>{
        setMarkOpen(false);
        markNewUnavailable()

    }

    const markNewUnavailable = event=>{
        //event.preventDefault();
        const user_id = localStorage.getItem("user_id");
        const data ={
            start_date : booking_start_date,
            start_time : booking_start_time,
            finish_date : booking_finish_date,
            finish_time : booking_finish_time,
        };
        console.log(data)
        Axios.post(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/${data.room_id}/unavailable-time-slot/`, data).then(
            res => {
                window.alert("Unavailable Time Slot has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert(err)
                console.log("Error:" + err)
            })

    }

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
    <Modal
            centered={false}
            open={mark_open}
            onClose={() => setMarkOpen(false)}
            onOpen={() => setMarkOpen(true)}
            
        >
            <Modal.Header>Mark Unavailable</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form>
                    <Form.Input
                        id='StartDate'
                        label='StartDate'
                        type='date'
                        onChange={(event) => {
                            set_booking_start_date(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='StartTime'
                        label='StartTime'
                        type='text'
                        placeholder='00:00'
                        onChange={(event) => {
                            set_booking_start_time(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='EndDate'
                        label='EndDate'
                        type='date'
                        onChange={(event) => {
                            set_booking_finish_date(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='EndTime'
                        label='EndTime'
                        type='text'
                        placeholder='00:00'
                        onChange={(event) => {
                            set_booking_finish_time(event.target.value)
                        }}
                    />
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={handleMarkClick}>Create</Button>
            </Modal.Actions>
        </Modal>


    <Container fluid>
        <Button
            fluid
            onClick={() => {setMarkOpen(true)}}
        > Mark as unavailable
        </Button>
    </Container>

    </Container>
        </Segment>
    )

}
export default RoomSchedule;
