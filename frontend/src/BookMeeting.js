import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';



// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function BookMeeting(){
    const [dates, setDates] = useState([]);
    const [openBook, setOpenBook] = useState(false);
    const [openMark, setOpenMark] = useState(false);
    const localizer = momentLocalizer(moment)

    const bookNewMeeting = event => {

    }

    const markUnavailable = event => {

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
            openBook={openBook}
            onCloseBook={() => setOpenBook(false)}
            onOpenBook={() => setOpenBook(true)}
        >
            <Modal.Header>Create New Meeting</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form>
                    <Form.Input
                        id='Name'
                        label='Name'
                        onChange={(event) => {
                            //set_name(event.target.value); //TODO: create set name
                        }}
                    />
                    <Form.Input
                        id='Date'
                        label='Date'
                        onChange={(event) => {
                            // TODO: ADD DATE FUNCTIONALITY
                        }}
                    />
                    <Form.Input
                        id='Invitees'
                        label='Invitees'
                        onChange={(event) => {
                            //set_invitees(event.target.value) //TODO: set invitees list
                        }}
                    />
                    <Form.Input
                        id='Room-id'
                        label='Room id'
                        onChange={(event) => {
                            //set_room_id(event.target.value)
                        }}
                    />
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenBook(false)}>Create</Button>
                <Button content='BookNewMeeting' primary onClick={bookNewMeeting}/>
            </Modal.Actions>
        </Modal>
    <Container fluid>

    <Button
        fluid
        onClick={() => {setOpen(true)}}
    > Book Meeting </Button>
    
    <Modal
        centered={false}
        open={open}
        onClose={() => setOpen(false)}
        onOpen={() => setOpen(true)}
    >
        <Modal.Header>Mark Unavailable</Modal.Header>
        <Modal.Content>
            <Modal.Description>
                <Form>
                <Form.Input
                    id='Date'
                    label='Date'
                    onChange={(event) => {
                        // TODO: ADD DATE FUNCTIONALITY
                    }}
                />
                <Form.Input
                    id='Time'
                    label='Time'
                    onChange={(event) => {
                        // TODO: ADD time FUNCTIONALITY
                    }}
                />
                </Form>
            </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
            <Button onClick={() => setOpen(false)}>Create</Button>
            <Button content='MarkUnavailable' primary onClick={markUnavailable}/>
        </Modal.Actions>
    </Modal>
    <Button
        fluid
        onClick={() => {setOpen(true)}}
    > Mark as unavailable</Button>
    </Container>
    </Container>


}
export default BookMeeting;
