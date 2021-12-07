import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment, TextArea} from "semantic-ui-react";
import Axios from "axios";

function UserSchedule() {
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
        user_id: localStorage.getItem("user_id")
    }
        Axios.get('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/unavailable-time-users/' + data.user_id)
            .then(function (response) {
                console.log(response.data);
                let appointments = response.data;
                for (let i = 0; i < appointments.length; i++) {
                    evs.push({
                        'title': appointments[i].booking_name,
                        'allDay': false,
                        'start': new Date(appointments[i].start_time),
                        'end': new Date(appointments[i].finish_time)
                    })
                }
            }).catch(
                err => {
                    console.log(err)
                })


    const handleMarkClick = () =>{
        setMarkOpen(false);
        markNewUnavailable()

    }

    const markNewUnavailable = event=>{
        const user_id = localStorage.getItem("user_id");
        const data ={
            start_date : booking_start_date,
            start_time : booking_start_time,
            finish_date : booking_finish_date,
            finish_time : booking_finish_time,
        };
        console.log(data)
        Axios.post(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/${user_id}/unavailable-time-slot/`, data).then(
            res => {
                window.alert("Success: Unavailable Event has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert("Failed: Unavailable Event Creation.")
                console.log(err)
            })

    }

    return <Container style={{ height: 800 }}>
        <br/><br/>
        <Calendar
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
            <Modal.Header>Create Unavailable Event:</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form>
                    <Form.Input
                        id='StartDate'
                        label='StartDate'
                        icon={'calendar alternate outline'}
                        iconPosition={'left'}
                        type='date'
                        onChange={(event) => {
                            set_booking_start_date(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='StartTime'
                        label='StartTime'
                        type='text'
                        icon={'clock outline'}
                        iconPosition={'left'}
                        placeholder='00:00'
                        onChange={(event) => {
                            set_booking_start_time(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='EndDate'
                        label='EndDate'
                        type='date'
                        icon={'calendar alternate outline'}
                        iconPosition={'left'}
                        onChange={(event) => {
                            set_booking_finish_date(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='EndTime'
                        label='EndTime'
                        type='text'
                        icon={'clock outline'}
                        iconPosition={'left'}
                        placeholder='00:00'
                        onChange={(event) => {
                            set_booking_finish_time(event.target.value)
                        }}
                    />
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button primary onClick={handleMarkClick}>Create </Button>
            </Modal.Actions>
        </Modal>
        <br/>
    <Container fluid>
        <Button secondary
                style={{
                    height: "50%"
                }}
            fluid
            onClick={() => {setMarkOpen(true)}}
        > Create Unavailable Event
        </Button>
    </Container>
    </Container>

}
export default UserSchedule;
