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
import UserStatistics from "./UserStatistics";
import RoomAvailability from "./RoomAvailability";
import WhoBookedRoom from "./WhoBookedRoom";
import UserAvailability from "./UserAvailability";
import {useNavigate} from 'react-router-dom';
import CreateRoom from "./CreateRoom";


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
            menuItem: 'Create Room', render: () => <CreateRoom/>
        },
        {
            menuItem: 'User Schedule', render: () => <UserSchedule/>
        },
        {
            menuItem: 'Room Schedule', render: () => <RoomSchedule/>
        },
        {
            menuItem: 'User Statistics', render: () => <UserStatistics/>
        },
        {
            menuItem: 'Room Management', render: () => <Tab.Pane active={isAuth}><BookMeeting/></Tab.Pane>
          
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
            menuItem :  <Button secondary onClick={() => {window.location.href ="/Dashboard"}}>Dashboard</Button>
        },
        {
            menuItem :  <Button onClick={logout}>Log Out</Button>
        },
    ]

   return (
       <Tab panes={panes}/>
        )
}
export default UserView;
