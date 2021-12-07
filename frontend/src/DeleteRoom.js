import React, {useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';
import Axios from "axios";

function DeleteRoom() {

    const [room_id, set_room_id] = useState("");

    const deleteRoom = event => {
        event.preventDefault();

        Axios.delete("https://coqui-bookings-database.herokuapp.com/coqui-bookings/Room/rooms/" + room_id).then(
            res => {
                window.alert("Room deleted successfully.")
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
                                id='room_id'
                                type={'number'}
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
        </Segment>
    )
}
export default DeleteRoom;
