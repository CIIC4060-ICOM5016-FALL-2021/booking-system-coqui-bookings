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
    const [booking_id, set_booking_id] = useState("");
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
        Axios.post(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/user/${user_id}/create`, data).then(
            res => {
                window.alert("Meeting has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert(err)
                console.log("Error:" + err)
            })

    }
    //add update meeting only name
    const updateMeeting = event=> {
        //event.preventDefault();
        const user_id = localStorage.getItem("user_id");
        const data ={
            booking_name : booking_name
        };
        console.log(data)
        Axios.put(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/${booking_id}/updateName`, data).then(
            res => {
                window.alert("Meeting has been updated.")
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
        events={evs}
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
        <Container fluid>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>

    </Container>
    <hr/>
        <Grid columns={2} relaxed='very' stackable>
            <Grid.Column>
                <Form>
                    <Form.Input
                        id='Name'
                        label='Name'
                        onChange={(event) => {
                            set_booking_name(event.target.value); 
                        }}
                    />
                    <Form.Input
                        id='Meeting Id'
                        label='Meeting Id'
                        onChange={(event) => {
                            set_booking_id(event.target.value); 
                        }}
                    />
                </Form>
            </Grid.Column>
            <Grid.Column>
                <Button content={'Update Meeting'} primary  onClick={updateMeeting}/>
            </Grid.Column>
        </Grid>

    </Container>


}
export default BookMeeting;
