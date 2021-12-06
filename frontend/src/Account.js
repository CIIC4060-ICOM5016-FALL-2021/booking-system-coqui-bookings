import React, {useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import Axios from "axios";

function Account() {

    const [user_email, set_email] = useState("");
    const [user_password, set_password] = useState("");
    const [user_first_name, set_first_name] = useState("");
    const [user_last_name, set_last_name] = useState("");

    const update = event => {
        event.preventDefault();

        const user_id = localStorage.getItem("user_id")
        const data = {
            user_email: user_email,
            user_password: user_password,
            user_first_name: user_first_name,
            user_last_name: user_last_name,
            role_id: role_id,
        };
        console.log(data)
        Axios.put("coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/" + user_id, data).then(
            res => {
                window.alert("User credentials have been updated.")
                console.log(res)
            }).catch(
            err => {
                console.log("Error:" + err)
            })
    }
    return (<Segment>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                id='user_email'
                                icon='user'
                                iconPosition='left'
                                label='Email'
                                onChange={(event) => {
                                    set_email(event.target.value);}}
                            />
                            Reminder: Email will be your accounts username when you log in next time.
                            <Form.Input
                                id='user_password'
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                                onChange={(event) => {
                                    set_password(event.target.value);}}
                            />
                            <Form.Input
                                id='user_first-name'
                                icon='user'
                                iconPosition='left'
                                label='First Name'
                                onChange={(event) => {
                                    set_first_name(event.target.value);}}
                            />
                            <Form.Input
                                id='user_last-name'
                                icon='user'
                                iconPosition='left'
                                label='Last Name'
                                onChange={(event) => {
                                    set_last_name(event.target.value);}}
                            />
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle' >
                        <Button content='Update User' icon='signup' size='big' onClick={update}/>
                    </Grid.Column>
                </Grid>
        </Segment>
    )
}
export default Account;
