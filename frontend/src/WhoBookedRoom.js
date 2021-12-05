import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment, TextArea} from "semantic-ui-react";
import Axios from "axios";


    function WhoBookedRoom(){

        const [room_id, set_room_id] = useState("");
        const [booking_start_date, set_booking_start_date] = useState("");
        const [booking_start_time, set_booking_start_time] = useState("");
        const [booking_finish_date, set_booking_finish_date] = useState("");
        const [booking_finish_time, set_booking_finish_time] = useState("");

        const booking_date_time_frame = {

            booking_start_time: booking_start_time,
            booking_start_date: booking_start_date,
            booking_finish_date: booking_finish_date,
            booking_finish_time: booking_finish_time,
        }
        let user = ""
        let textarea_user = document.getElementById("textarea_user");

        function getUserWhoAppointedRoomAtTimeFrame() {
            console.log(booking_date_time_frame)
            Axios.post('https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/User/TimeFrame/' + room_id, booking_date_time_frame)
                .then(function (response) {
                    console.log(response.data);
                    user = response.data;
                    textarea_user.value = JSON.stringify(user)
                }).catch(
                err => {
                    console.log(err)
                })
        }
        return (<Segment>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <h3>Find User Who Appointed A Room At A Given Time Frame:</h3>
                        <Form>
                            <Form.Input
                                id='room_id'
                                icon='room'
                                iconPosition='left'
                                label='Room Id'
                                placeholder='Room Id'
                                onChange={(event) => {
                                    set_room_id(event.target.value);
                                }}
                            />
                            <Form.Input
                                id='booking_start_date'
                                icon='date'
                                iconPosition='left'
                                label='Start Date'
                                placeholder='date'
                                type='date'
                                onChange={(event) => {
                                    set_booking_start_date(event.target.value);
                                }}
                            />
                            <Form.Input
                                id='booking_start_time'
                                icon='time'
                                ampm={false}
                                iconPosition='left'
                                label='Start Time'
                                placeholder='00:00'
                                //type='time'
                                onChange={(event) => {
                                    set_booking_start_time(event.target.value);
                                }}
                            />
                            <Form.Input
                                id='booking_finish_date'
                                icon='date'
                                iconPosition='left'
                                label='Finish Date'
                                placeholder='date'
                                type='date'
                                onChange={(event) => {
                                    set_booking_finish_date(event.target.value);
                                }}
                            />
                            <Form.Input
                                id="booking_finish_time"
                                icon='time'
                                ampm={false}
                                iconPosition='left'
                                label='Finish Time'
                                placeholder='00:00'
                                //type='time'
                                onChange={(event) => {
                                    set_booking_finish_time(event.target.value);
                                }}
                            />
                        </Form>
                    </Grid.Column>
                    <Grid.Column>
                        <Form>
                            <Button content='Get User' style={{marginTop: 28}} primary
                                    onClick={getUserWhoAppointedRoomAtTimeFrame}/>
                        </Form>
                    </Grid.Column>
                </Grid>
                <TextArea
                    id={'textarea_user'}
                    style={{
                        cursor: "text",
                        width: "48%",
                        height: "50%"
                    }}
                    value={user}
                    placeholder="User"
                    disabled
                />
            </Segment>

        )
    }
export default WhoBookedRoom
