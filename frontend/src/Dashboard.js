import React from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import {Container} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import Axios from "axios";

function Dashboard(){


    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/busiest-times`)
        .then(function (response) {
            localStorage.removeItem('data_busiest_times')
            let data_busiest_times = []
            let busiest_times = response.data;
            for (let i = 0; i < busiest_times.length; i++) {
                data_busiest_times.push({
                    "name" : busiest_times[i].start_time+"-"+busiest_times[i].finish_time,
                    "busiest_times": busiest_times[i].times_booked
                })
            }
            localStorage.setItem('data_busiest_times',JSON.stringify(data_busiest_times))

        }).catch(
            err => {
                console.log(err)
    })
    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/most-booked-users`)
        .then(function (response) {
            localStorage.removeItem('data_most_booked_user')
            let data_most_booked_user = []
            let most_booked = response.data;
            for (let i = 0; i < most_booked.length; i++) {
                data_most_booked_user.push({
                    "user_id" : most_booked[i].user_id,
                    "most_booked_user": most_booked[i].times_booked
                })
            }
            localStorage.setItem('data_most_booked_user',JSON.stringify(data_most_booked_user))
        }).catch(
            err => {
                console.log(err)
    })
    Axios.get(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Booking/bookings/most-booked-rooms`)
    .then(function (response) {
        localStorage.removeItem('data_most_booked_room')
        let data_most_booked_room = []
        let most_booked = response.data;
        for (let i = 0; i < most_booked.length; i++) {
            data_most_booked_room.push({
                "room_id" : most_booked[i].room_id,
                "most_booked_room": most_booked[i].times_booked
            })
        }
        localStorage.setItem('data_most_booked_room',JSON.stringify(data_most_booked_room))
    }).catch(
        err => {
            console.log(err)
    })

    const data_busiest_times = JSON.parse(localStorage.getItem('data_busiest_times'))
    const data_most_booked_user = JSON.parse(localStorage.getItem('data_most_booked_user'))
    const data_most_booked_room = JSON.parse(localStorage.getItem('data_most_booked_room'))

    return <Container style={{ height: 800 }}>

        <BarChart width={730} height={250} data={data_busiest_times}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="busiest_times" fill="#8884d8" />
        </BarChart>
        <BarChart width={730} height={250} data={data_most_booked_user}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="user_id" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="most_booked_user" fill="#8884d8" />
        </BarChart>
        <BarChart width={730} height={250} data={data_most_booked_room}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="room_id" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="most_booked_room" fill="#8884d8" />
        </BarChart>
    </Container>

}

export default Dashboard;
