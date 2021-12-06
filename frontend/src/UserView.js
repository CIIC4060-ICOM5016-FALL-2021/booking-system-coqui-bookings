import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
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


function UserView(){
    const logout = event => {
        event.preventDefault();
        window.alert("User has been logged out.")
        localStorage.clear()
        window.setInterval('window.location.href = "/"', 1000);

    }
    const data = {
        user_id: localStorage.getItem("user_id"),
        role_id: localStorage.getItem("role_id")
    }

    const [isAuth, setIsAuth] = useState(false)

    // add create room and delete room

    // move mark as un to user schedule
    // add mark as un to room schedule
    
    if (data.role_id === 3){

        const panes = [
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
                menuItem :  <Button onClick={logout}>Log Out</Button>
            },
        ]
    }else{
        const panes = [
            {
                menuItem: 'User Schedule', render: () => <UserSchedule/>
            },
            {
                menuItem: 'User Statistics', render: () => <UserStatistics/>
            },
            {
                menuItem: 'User Availability', render: () => <UserAvailability/>

            },
            {
                menuItem: 'Account', render: () => <Account/>
            },
            {
                menuItem :  <Button onClick={logout}>Log Out</Button>
            },
        ]
    }

   return (
       <Tab panes={panes}/>
    )

    
}
export default UserView;
