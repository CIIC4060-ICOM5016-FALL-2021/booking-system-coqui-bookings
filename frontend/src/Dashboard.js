import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import { data } from 'jquery';
import Axios from "axios";



function Dashboard(){

    //top five busiest hours
    //const [data_busiest_times, setBusiestTimes] = useState([{"name": 1, "Counts": 5},
                                                // {"name": 2, "Counts": 4},
                                                // {"name": 3, "Counts": 3},
                                                // {"name": 4, "Counts": 2},
                                                // {"name": 5, "Counts": 1}]);
    const data_busiest_times = []
    const data_most_booked_user = []
    const data_most_booked_room = []

    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/busiest-times`)
        .then(function (response) {
            let busiest_times = response.data;
            for (let i = 0; i < busiest_times.length; i++) {
                data_busiest_times.push({
                    "name" : busiest_times[i].start_time+"-"+busiest_times[i].finish_time,
                    "times_booked": busiest_times[i].times_booked
                })
            }
        }).catch(
            err => {
                console.log(err)
    })
    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/most-booked-users`)
        .then(function (response) {
            let most_booked = response.data;
            for (let i = 0; i < most_booked.length; i++) {
                data_most_booked_user.push({
                    "user_id" : most_booked[i].user_id,
                    "times_booked": most_booked[i].times_booked
                })
            }
        }).catch(
            err => {
                console.log(err)
    })
    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/most-booked-rooms`)
    .then(function (response) {
        let most_booked = response.data;
        for (let i = 0; i < most_booked.length; i++) {
            data_most_booked_room.push({
                "room_id" : most_booked[i].user_id,
                "times_booked": most_booked[i].times_booked
            })
        }
    }).catch(
        err => {
            console.log(err)
    })
    
    return <Container style={{ height: 800 }}>

        <BarChart width={730} height={250} data={data_busiest_times}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="times_booked" fill="#8884d8" />
        </BarChart>
        <BarChart width={730} height={250} data={data_most_booked_user}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="most_booked_user" fill="#8884d8" />
        </BarChart>
        <BarChart width={730} height={250} data={data_most_booked_room}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="most_booked_room" fill="#8884d8" />
        </BarChart>
    </Container>


}

export default Dashboard;
