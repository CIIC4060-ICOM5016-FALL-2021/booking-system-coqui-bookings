import React, {Component, useState} from 'react';
import {Calendar, dateFormat, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Segment} from "semantic-ui-react";
import Axios from "axios";


function Schedule(){

    const [date, set_date] = useState("");
    
    const data = {
        date : date,
        user_id: localStorage.getItem("user_id")
    }
    const getUserSchedule = event => {
        Axios.post('http://127.0.0.1:5000/coqui-bookings/User/users/' + data.user_id +'/schedule', data)
            .then( res => {
                console.log(res.data)
            }
    ).catch (err => {
            return "NOT FOUND ERROR";
        })
 }
  return( <Segment>   <Grid columns={2} relaxed='very' stackable>
      <Grid.Column>
          <Form>
              <Form.Input
                  id = 'date'
                  icon='date'
                  iconPosition='left'
                  label='Date'
                  placeholder='Date'
                  type='date'
                  onChange={(event) => {
                  set_date(event.target.value);}}
              />
          </Form>
          </Grid.Column>
      <Grid.Column>
          <Form>
              <Button content='Get Schedule' style={{marginTop:28}} primary onClick={getUserSchedule}/>
          </Form>
      </Grid.Column>
      </Grid>
        </Segment>
  )
}
export default Schedule;
