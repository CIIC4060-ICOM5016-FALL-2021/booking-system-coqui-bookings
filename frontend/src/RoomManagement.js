import React, {useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import Axios from "axios";

function RoomManagement() {

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
                window.alert("Success: Room has been created.")
                console.log(res)
            }).catch(
            err => {
                window.alert("Failed: Room creation.")
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
                window.alert("Success: Room has been updated.")
                console.log(res)
            }).catch(
            err => {
                window.alert("Failed: Room update.")
                console.log(err)
            })
    }
    const deleteRoom = event => {
        event.preventDefault();

        Axios.delete("https://coqui-bookings-database.herokuapp.com/coqui-bookings/Room/rooms/" + room_id).then(
            res => {
                window.alert("Success: Room has been deleted.")
                console.log(res)
            }).catch(
            err => {
                window.alert("Failed: Room Deletion.")
                console.log("Error:" + err)
            })
    }

    return (<Segment>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <h2>Create Room:</h2>
                            <Form.Input
                                id='room_name'
                                icon='building outline'
                                iconPosition='left'
                                label='Room Name'
                                type='text'
                                onChange={(event) => {
                                    set_room_name(event.target.value);}}
                            />
                            <Form.Input
                                id='room_type_id'
                                icon='building outline'
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
            <br/><br/>
            <hr/>
            <br/>
        <Grid columns={2} relaxed='very' stackable>
            <Grid.Column>
                <Form>
                    <h2>Update Room:</h2>
                    <Form.Input
                        id='room_name'
                        icon='building outline'
                        iconPosition='left'
                        label='Room Name'
                        type='text'
                        onChange={(event) => {
                            set_room_name(event.target.value);}}
                    />
                    <Form.Input
                        id='room_type_id'
                        icon='building outline'
                        type={'number'}
                        iconPosition='left'
                        label='Room Type Id'
                        onChange={(event) => {
                            set_room_type_id(event.target.value);}}
                    />
                    <Form.Input
                        id='room_id'
                        icon='building outline'
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
            <br/><br/>
            <hr/>
            <br/>
            <Grid columns={2} relaxed='very' stackable>
                <Grid.Column>
                    <h2>Delete Room:</h2>
                    <Form>
                        <Form.Input
                            id='room_id'
                            type={'number'}
                            icon ={"building outline"}
                            iconPosition='left'
                            label='Room Id'
                            onChange={(event) => {
                                set_room_id(event.target.value);}}
                        />
                    </Form>
                </Grid.Column>
                <Grid.Column>
                    <Button content={'Delete Room'} primary  onClick={deleteRoom}/>
                </Grid.Column>
            </Grid>
            <br/>
            <br/>
    </Segment>
    )
}
export default RoomManagement;
