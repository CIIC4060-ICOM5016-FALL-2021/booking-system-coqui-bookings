import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import Axios from "axios";



// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function BookMeeting(){
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




    const handleBookClick = () =>{
        setOpen(false);
        bookNewMeeting()

    }

    const bookNewMeeting = event=> {
        //event.preventDefault();
        const user_id = localStorage.getItem("user_id");
        const data ={
            booking_name : booking_name,
            booking_start_date : booking_start_date,
            booking_start_time : booking_start_time,
            booking_finish_date : booking_finish_date,
            booking_finish_time : booking_finish_time,
            booking_invitee_id : booking_invitee_id,
            room_id : room_id
        };
        console.log(data)
        Axios.post(`http://127.0.0.1:5000/coqui-bookings/Booking/bookings/user/${user_id}/create`, data).then(
            res => {
                window.alert("Meeting has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert(err)
                console.log("Error:" + err)
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
        Axios.post(`http://127.0.0.1:5000/coqui-bookings/User/${user_id}/unavailable-time-slot/`, data).then(
            res => {
                window.alert("Unavailable Time Slot has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert(err)
                console.log("Error:" + err)
            })

    }


    return <Container style={{ height: 800 }}><Calendar
        selectable
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
        onSelecting = {(selected) =>{ setDates([{
                        'title': 'Selection',
                        'allDay': false,
                        'start': new Date(selected.start),
                        'end': new Date(selected.end)
                    }] ) } }
    >

    </Calendar>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}

        >
            <Modal.Header>Create New Meeting</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form>
                    <Form.Input
                        id='Name'
                        label='Name'
                        onChange={(event) => {
                            set_booking_name(event.target.value); 
                        }}
                    />
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
                        type='time'
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
                        type='time'
                        onChange={(event) => {
                            set_booking_finish_time(event.target.value)
                        }}
                    />
                    <Form.Input
                        id='Invitees'
                        label='Invitees'
                        onChange={(event) => {
                            set_booking_invitee_id(event.target.value) 
                        }}
                    />
                    <Form.Input
                        id='Room-id'
                        label='Room id'
                        type='number'
                        onChange={(event) => {
                            set_room_id(event.target.value)
                        }}
                    />
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={handleBookClick}>Create</Button>
            </Modal.Actions>
        </Modal>

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
                        type='time'
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
                        type='time'
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
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>
        <Button
            fluid
            onClick={() => {setMarkOpen(true)}}
        > Mark as unavailable</Button>

    </Container>
    </Container>


}
export default BookMeeting;
