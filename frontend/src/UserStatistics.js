import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Icon, Statistic} from "semantic-ui-react";
import Axios from "axios";

import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";


function UserStatistics(){

    const user_id=localStorage.getItem("user_id")

    // const [invitee_id, set_invitee_id] = useState("");
    // const [room_id, set_room_id] = useState("");
    // const invitee_id = ""
    // const room_id = ""

    //const get_invitee_id = () => {

        Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/${user_id}/invitee-most-booked-with`)
            .then(function (response) {
                console.log(response.data);
                //set_invitee_id(response.data);
                let invitee_id=response.data
                //return invitee_id

            }).catch(
                err => {
                    console.log("Error:" + err)
            })
    //}

    //const get_room_id = () => {
        Axios.get("https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/"+ user_id +"/most_used_room")
            .then(function (response) {
                console.log(response.data);
                let room_id = response.data
                // set_room_id(response.data);  
                // room_id=response.data
                //return room_id

            }).catch(
                err => {
                    console.log("Error:" + err)
            })
        //}

    return (<Container style={{ height: 800 }}>
        
        <Statistic>
            <Statistic.Value></Statistic.Value>
            <Statistic.Label>Most Used Room By User</Statistic.Label>
        </Statistic>

        <Statistic>
            <Statistic.Value></Statistic.Value>
            <Statistic.Label>User Most Booked With</Statistic.Label>
        </Statistic>
    </Container>)


}

export default UserStatistics;
