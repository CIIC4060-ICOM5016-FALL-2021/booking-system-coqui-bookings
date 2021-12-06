import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Divider, Form, Grid, Header, Modal, Segment, Tab} from "semantic-ui-react";
import BookMeeting from "./BookMeeting";
import UserSchedule from "./UserSchedule";
import HomePage from "./HomePage";
import Axios from "axios";
import Account from "./Account";
import RoomSchedule from "./RoomSchedule";
import RoomAvailability from "./RoomAvailability";
import WhoBookedRoom from "./WhoBookedRoom";
import UserAvailability from "./UserAvailability";
import {useNavigate} from 'react-router-dom';

function UserView(){
    const logout = event => {
        event.preventDefault();
        window.alert("User has been logged out.")
        localStorage.clear()
        window.setInterval('window.location.href = "/"', 1000);

    }
    const [isAuth, setIsAuth] = useState(false)
    const panes = [
        {
            menuItem: 'User Schedule', render: () => <UserSchedule/>
        },
        {
            menuItem: 'Room Schedule', render: () => <RoomSchedule/>
        },
        {
            menuItem: 'Room Availability', render: () => <RoomAvailability/>

        },
        {
            menuItem: 'User Availability', render: () => <UserAvailability/>

        },
        {
            menuItem: 'Booking', render: () => <BookMeeting/>
        },
        {
            menuItem: 'Booked Room', render: () => <WhoBookedRoom/>
        },
        {
            menuItem: 'Account', render: () => <Account/>
        },
        {
            menuItem :  <Button onClick={logout}>Log Out</Button>
        },
        {
            menuItem :  <Button secondary onClick={() => {window.location.href ="/Dashboard"}}>Dashboard</Button>
        },
    ]

   return (
       <Tab panes={panes}/>
        )
}
export default UserView;
