import React, {useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import Axios from "axios";
import $ from 'jquery';
import {useNavigate} from "react-router-dom";

function HomePage() {
    let navigate = useNavigate();
    const [open, setOpen] = useState(false);
    console.log(open);
    const handleChange = (event, newValue) => {
        setOpen(true);
    }
    const [user_email, set_email] = useState("");
    const [user_password, set_password] = useState("");
    const [user_first_name, set_first_name] = useState("");
    const [user_last_name, set_last_name] = useState("");
    const [role_id, set_role_id] = useState("");

    const signUp = event => {
        event.preventDefault();
        const data = {
            user_email: user_email,
            user_password: user_password,
            user_first_name: user_first_name,
            user_last_name: user_last_name,
            role_id: role_id
        };
        console.log(data)
        Axios.post("https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users", data).then(
            res => {
                window.alert("Success: User has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert(err)
                console.log(err)
            })
    }

    const logIn = event => {
        event.preventDefault();
        const data = {
            user_email: user_email,
            user_password: user_password,
        };
        console.log(data)
        Axios.post("https://coqui-bookings-database.herokuapp.com/coqui-bookings/User/users/login", data).then(
            res => {
                window.alert("Success: User has been logged in.")
                window.setInterval('window.location.href = "/UserView"', 1000);
                localStorage.setItem("user_email",  user_email);
                localStorage.setItem("user_password", user_password);
                localStorage.setItem("user_id", res.data[1]);
                localStorage.setItem("role_id",  res.data[2]);

                console.log(res.data)
            }).catch(
            err => {
                console.log(err)
                window.alert(err)
            })
    }

    localStorage.setItem("role_id",  role_id);


    return (<Segment><Header dividing textAlign="center" size="huge">Welcome to Coqui Bookings</Header>
            <Modal
                centered={false}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>Account Credentials</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
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
                             <Form.Input
                                 id='role_id'
                                 icon='exclamation triangle'
                                 iconPosition='left'
                                 label='Role'
                                 type='number'
                                 onChange={(event) => {
                                     set_role_id(event.target.value);}}
                             />
                        </Form>
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={signUp}>Sign Up</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                id = 'user_email_login'
                                icon='user'
                                iconPosition='left'
                                label='Email'
                                placeholder='Email'
                                onChange={(event) => {
                                    set_email(event.target.value);}}
                            />
                            <Form.Input
                                id = 'user_password_login'
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                                onChange={(event) => {
                                    set_password(event.target.value);}}
                            />
                            <Button content='Login' primary onClick={logIn}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle' >
                        <Button content='Sign up' icon='signup' size='big' onClick={handleChange}/>
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
                <div className="HomePage">
                    <img src={require('./images/coqui.png').default} height={200} width={200}/>
                </div>
            </Segment>
        </Segment>
    )
}

export default HomePage;
