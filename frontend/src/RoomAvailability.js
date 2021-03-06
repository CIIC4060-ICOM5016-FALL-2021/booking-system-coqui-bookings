import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment, TextArea} from "semantic-ui-react";
import Axios from "axios";


    function RoomAvailability(){

    const [start_date, set_start_date] = useState("");
    const [start_time, set_start_time] = useState("");
    const [finish_date, set_finish_date] = useState("");
    const [finish_time, set_finish_time] = useState("");

        const date_time_frame = {
            start_date: start_date,
            start_time: start_time,
            finish_date: finish_date,
            finish_time: finish_time,
        }
        const rooms = []
        let textarea = document.getElementById("textarea");

        function getRoomsAvailableAtTimeFrame() {
            if (rooms.length !== 0) {
                const len = rooms.length
                for (let i = 0; i < len; i++) {
                    rooms.pop()
                }
            }
            console.log(date_time_frame)
            Axios.post('https://coqui-bookings-database.herokuapp.com/coqui-bookings/Room/rooms/verifytimeframe', date_time_frame)
                .then(function (response) {
                    console.log(response.data);
                    let room = response.data;
                    for (let i = 0; i < room.length; i++) {
                        rooms.push({
                            'room_id': room[i].room_id,
                            'room_name': room[i].room_name,
                            'room_type_id': room[i].room_type_id
                        })
                    }
                    textarea.value = JSON.stringify(rooms)
                }).catch(
                err => {
                    window.alert(err)
                    console.log(err)
                })
        }
        return (<Segment>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <h2>All Available Rooms At A Given Time Frame:</h2>
                        <Form>
                            <Form.Input
                                id='start-date'
                                icon={'calendar alternate outline'}
                                iconPosition={'left'}
                                label='Start Date'
                                placeholder='date'
                                type='date'
                                onChange={(event) => {
                                    set_start_date(event.target.value);
                                }}
                            />
                            <Form.Input
                                id='start-time'
                                icon={'clock outline'}
                                iconPosition={'left'}
                                label='Start Time'
                                placeholder='00:00'
                                //type='time'
                                onChange={(event) => {
                                    set_start_time(event.target.value);
                                }}
                            />
                            <Form.Input
                                id='finish-date'
                                icon={'calendar alternate outline'}
                                iconPosition={'left'}
                                label='Finish Date'
                                placeholder='date'
                                type='date'
                                onChange={(event) => {
                                    set_finish_date(event.target.value);
                                }}
                            />
                            <Form.Input
                                icon={'clock outline'}
                                iconPosition={'left'}
                                label='Finish Time'
                                placeholder='00:00'
                                //type='time'
                                onChange={(event) => {
                                    set_finish_time(event.target.value);
                                }}
                            />
                        </Form>
                    </Grid.Column>
                    <Grid.Column>
                        <Form>
                            <Button content='Get Available Rooms' style={{marginTop: 28}} primary
                                    onClick={getRoomsAvailableAtTimeFrame}/>
                        </Form>
                    </Grid.Column>
                </Grid>
                <br/><br/>
                    <TextArea
                        id={'textarea'}
                        style={{
                            cursor: "text",
                            width: "48.6%",
                            height: "50%"
                        }}
                        value={rooms}
                        placeholder="Available Rooms"
                        disabled
                    />
                    <br/><br/>
            </Segment>

        )
    }
export default RoomAvailability
