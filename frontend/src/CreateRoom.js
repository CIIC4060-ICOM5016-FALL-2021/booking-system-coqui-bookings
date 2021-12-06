import React, {useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import Axios from "axios";

function CreateRoom() {

    const [room_name, set_room_name] = useState("");
    const [room_type_id, set_room_type_id] = useState("");
    const [room_id, set_room_id] = useState("");


    const createRoom = event => {
        event.preventDefault();
        
        const data = {
            room_name: room_name,
            room_type_id: room_type_id,
        };
        console.log(data)
        Axios.post("https://coqui-bookings-database.herokuapp.com/coqui-bookings/Room/rooms", data).then(
            res => {
                window.alert("Room created successfully.")
                console.log(res)
            }).catch(
            err => {
                console.log(err)
            })
    }

    const updateRoom = event => {
        event.preventDefault();

        const data = {
            room_name: room_name,
            room_type_id: room_type_id,
        };
        console.log(data)
        Axios.put(`https://coqui-bookings-database.herokuapp.com/coqui-bookings/Room/rooms/${room_id}`, data).then(
            res => {
                window.alert("Room updated successfully.")
                console.log(res)
            }).catch(
            err => {
                console.log(err)
            })
    }

    return (<Segment>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                id='room_name'
                                icon='room'
                                iconPosition='left'
                                label='Room Name'
                                type='text'
                                onChange={(event) => {
                                    set_room_name(event.target.value);}}
                            />
                            <Form.Input
                                id='room_type_id'
                                icon='room'
                                type={'number'}
                                iconPosition='left'
                                label='Room Type Id'
                                onChange={(event) => {
                                    set_room_type_id(event.target.value);}}
                            />
                        </Form>
                    </Grid.Column>
                    <Grid.Column>
                        <Button content={'Create Room'} primary  onClick={createRoom}/>
                    </Grid.Column>
                </Grid>
            <hr/>
        <Grid columns={2} relaxed='very' stackable>
            <Grid.Column>
                <Form>
                    <Form.Input
                        id='room_name'
                        icon='room'
                        iconPosition='left'
                        label='Room Name'
                        type='text'
                        onChange={(event) => {
                            set_room_name(event.target.value);}}
                    />
                    <Form.Input
                        id='room_type_id'
                        icon='room'
                        type={'number'}
                        iconPosition='left'
                        label='Room Type Id'
                        onChange={(event) => {
                            set_room_type_id(event.target.value);}}
                    />
                    <Form.Input
                        id='room_id'
                        icon='room'
                        type={'number'}
                        iconPosition='left'
                        label='Room Id'
                        onChange={(event) => {
                            set_room_id(event.target.value);}}
                    />
                </Form>
            </Grid.Column>
            <Grid.Column>
                <Button content={'Update Room'} primary  onClick={updateRoom}/>
            </Grid.Column>
        </Grid>
    </Segment>
    )
}
export default CreateRoom;
