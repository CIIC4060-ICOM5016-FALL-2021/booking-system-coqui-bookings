import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Icon, Statistic} from "semantic-ui-react";
import Axios from "axios";

import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";


function UserStatistics(){

    const user_id=localStorage.getItem("user_id")

        Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/${user_id}/invitee-most-booked-with`)
            .then(function (response) {
                console.log(response.data);
                let invitee_id=response.data.user_first_name +" "+ response.data.user_last_name
                localStorage.setItem('invitee_id',invitee_id)

            }).catch(
                err => {
                    console.log("Error:" + err)
            })

        Axios.get("https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/"+ user_id +"/most_used_room")
            .then(function (response) {
                console.log(response.data);
                let room_id = response.data.room_name
                localStorage.setItem('room_id', room_id)

            }).catch(
                err => {
                    console.log("Error:" + err)
            })

    return (<Container style={{ height: 800 }}>
        <br/>
            <Card>
        <Card.Content>
        <Card.Header>Most Used Room By User</Card.Header>
        <Card.Description>
            {localStorage.getItem('room_id')}
        </Card.Description>
        </Card.Content>
    </Card>
    <Card>
    <Card.Content>
        <Card.Header>User Most Booked With</Card.Header>
        <Card.Description>
            {localStorage.getItem('invitee_id')}
        </Card.Description>
        </Card.Content>
    </Card>

    </Container>)


}

export default UserStatistics;
