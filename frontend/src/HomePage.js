import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import {useNavigate} from 'react-router-dom';


function HomePage() {
    let navigate = useNavigate();
    const [open, setOpen] = useState(false);
    console.log(open);
    const handleChange = (event, newValue) => {
        setOpen(true);
    }

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
                                icon='user'
                                iconPosition='left'
                                label='First Name'
                            />
                              <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Last Name'
                            />
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Email'
                            />
                              Reminder: Email will be your accounts username when you log in next time.
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                            />
                        </Form>
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => {navigate("/SelectScreen");}}>Login</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username'
                                placeholder='Username'
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                            />
                            <Button content='Login' primary onClick={() => {navigate("/SelectScreen");}}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle' >
                        <Button  content='Sign up' icon='signup' size='big' onClick={handleChange} />
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    )
}


export default HomePage;
