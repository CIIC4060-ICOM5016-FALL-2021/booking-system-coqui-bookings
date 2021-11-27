import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import {useNavigate} from 'react-router-dom';


function SelectScreen() {
    let navigate = useNavigate();
    const [open, setOpen] = useState(false);
    console.log(open);
    const handleChange = (event, newValue) => {
        setOpen(true);
    }

    return (<Segment><Header  textAlign="center" size="huge">Choose the option to proceed with
    <Button floated="right" content='Logout' icon='signup' size='big' onClick={() => {navigate.push("/Home");}}/></Header>
                <Grid columns={2} relaxed='very' stackable>

                    <Grid.Column verticalAlign='middle'>
                        <Button  content='DashBoard'  size='big' onClick={() => {navigate.push("/Dashboard");}}/>
                        <Button  content='UserView'  size='big' onClick={() => {navigate.push("/UserView");}}/>
                        <Button  content='Schedule'  size='big' onClick={() => {navigate.push("/SelectScreen");}}/>
                    </Grid.Column>
                </Grid>
            </Segment>
    )
}
export default SelectScreen;
