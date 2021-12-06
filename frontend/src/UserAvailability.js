import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment, TextArea} from "semantic-ui-react";
import Axios from "axios";


    function UserAvailaility(){

    const [date, set_date] = useState("");
    const [user_id_list, set_user_id_list] = useState("");
    let array = user_id_list.split(',')
        let list = []
        for( let i = 0; i<array.length; i++){
            list.push(
                parseInt(array[i].trim())
            )

        }
       let  result = ""
        const info = {
            date: date,
            user_id_list: list,
        }

        let textarea = document.getElementById("textarea");

        function getFreeTimeForUsers() {
            console.log(info)
            Axios.post('https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/free-time-for-users', info)
                .then(function (response) {
                    console.log(response.data);
                    result = response.data;
                    textarea.value = JSON.stringify(result)
                }).catch(
                err => {
                    console.log(err)
                })
        }
        return (<Segment>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <h2>Find Free Time For Users:</h2>
                        <Form>
                            <Form.Input
                                id='date'
                                icon='date'
                                iconPosition='left'
                                label='Date'
                                placeholder='date'
                                type='date'
                                onChange={(event) => {
                                    set_date(event.target.value);
                                }}
                            />
                            <Form.Input
                                id='user_id_list'
                                icon='user'
                                iconPosition='left'
                                label='Users'
                                placeholder='1, 2 ,3'
                                onChange={(event) => {
                                    set_user_id_list(event.target.value);
                                }}
                            />
                        </Form>
                    </Grid.Column>
                    <Grid.Column>
                        <Form>
                            <Button content='Get Free Time' style={{marginTop: 28}} primary
                                    onClick={getFreeTimeForUsers}/>
                        </Form>
                    </Grid.Column>
                </Grid>
                    <TextArea
                        id={'textarea'}
                        style={{
                            cursor: "text",
                            width: "48%",
                            height: "50%"
                        }}
                        value={result}
                        placeholder="Free Time for Users"
                        disabled
                    />
            </Segment>

        )
    }
export default UserAvailaility
