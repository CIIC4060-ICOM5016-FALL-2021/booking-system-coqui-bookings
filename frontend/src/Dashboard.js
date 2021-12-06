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

    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/busiest-times`)
        .then(function (response) {
            //console.log(response.data);
            let busiest_times = response.data;
            //data_busiest_times = []
            for (let i = 0; i < busiest_times.length; i++) {
                data_busiest_times.push({
                    "name" : busiest_times[i].start_time+"-"+busiest_times[i].finish_time,
                    "times_booked": busiest_times[i].times_booked
                })
            }
            //localStorage.setItem('most_booked',JSON.stringify(data_busiest_times))

        }).catch(
            err => {
                console.log(err)
    })
    
    console.log(data_busiest_times)
    
    return <Container style={{ height: 800 }}>

        <BarChart width={730} height={250} data={data_busiest_times}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="times_booked" fill="#8884d8" />
        </BarChart>
    </Container>


}

export default Dashboard;
