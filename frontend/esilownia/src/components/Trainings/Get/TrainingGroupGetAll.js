import React, {useEffect, useState} from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import axiosInstance from "../../Axios/Axios";
import Photo from '../../../imgs/gymcoin.png';
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";


function TrainingGroupGetAll() {

    const [trainingGroupAll, setTrainingGroupAll] = useState([]);
    const [trainingGroupTypeAll, setTrainingGroupTypeAll] = useState([]);
    const [typeSelected, setTypeSelected] = useState([]);
    const [trainingFilter, setTrainingFilter] = useState([]);


    const handleChange = (e) => {
        e.preventDefault();

        let cleanArray = []


        if (typeSelected.length === 0) {

            cleanArray = trainingGroupAll;
        } else {

            trainingGroupAll.map(function (training) {

                for (let j = 0; j < training.type.length; j++) {

                    for (let i = 0; i < typeSelected.length; i++) {

                        if (training.type[j].toString() === typeSelected[i]) {

                            cleanArray.push(training)

                        }
                    }
                }
            })
        }
        setTrainingFilter(cleanArray);
    }

    const typesChecked = (e) => {

        if (typeSelected.indexOf(e.target.name) !== -1) {
            let name = e.target.name;
            setTypeSelected(typeSelected.filter((e) => (e !== name)))
        } else {
            let name = e.target.name;
            setTypeSelected([...typeSelected, name]);
        }

    }


    useEffect(() => {

        axiosInstance
            .post(`training/group/all`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
                }
            })
            .then((res) => {
                setTrainingGroupAll(res.data)
                setTrainingFilter(res.data)
            });

        axiosInstance
            .post(`training/group/type/all`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
                }
            })
            .then((res) => {
                setTrainingGroupTypeAll(res.data)
            });

    }, []);
    return (
        <div className="trainingGroupGetAll">

            <div className="text-center">
                <hr></hr>
                <h1 style={{"fontSize": "5vw"}} className="display-1 font-weight-light mb-4">Wszystkie grupy</h1>
                <hr></hr>
            </div>

            <div className="container p-4 mx-auto border border-2"  id="tren_col">
                <h5 className="font-weight-light text-center">Typ Treningu:</h5>
                <Form className="row justify-content-start">
                    <hr width={'100%'} color={'black'}/>
                    {trainingGroupTypeAll.map((types) => (
                        <div key={`inline-checkbox-${types.id}`} className="form-check-inline mx-auto">
                            <Form.Check
                                inline
                                name={types.id}
                                type="checkbox"
                                onChange={typesChecked.bind(this)}
                                id={`inline-checkbox-${types.id}`}
                            /> {types.type.charAt(0).toUpperCase()+types.type.slice(1)}
                        </div>
                    ))}
                    <div className="col-md-3">
                    </div>
                    <hr width={'90%'} color={'black'}/>
                    <div className="container">
                        <Button onClick={handleChange} variant="btn btn-lg border">Filtruj</Button>
                    </div>
                </Form>
            </div>

            <div className="row p-4 border mb-4 mt-4 text-center flex" id="tren_container">
                {trainingFilter.map(function (cValue, idx) {

                    if (cValue.difficulty === "0") {
                        cValue.difficulty = "Łatwy"
                    }
                    if (cValue.difficulty === "1") {
                        cValue.difficulty = "Średni"
                    }
                    if (cValue.difficulty === "2") {
                        cValue.difficulty = "Trudny"
                    }
                    if (cValue.difficulty === "3") {
                        cValue.difficulty = "Armagedon"
                    }

                    return (
                        <div className="card m-1" id="karta_tren" key={idx}>
                            <img src={Photo} width="100%" height="width" className="card-img-top rounded-circle"
                                 alt="..."/>
                            <div className="card-body">
                                <div>
                                    <h5 className="card-title">{cValue.title}</h5>
                                    <div className="card-subtitle">
                                        {trainingGroupTypeAll.map(function (type, id) {
                                            for (let i = 0; i < cValue.type.length; i++) {
                                                if (cValue.type.includes(type.id)) {
                                                    return (<p key={id}>{type.type}</p>)
                                                }
                                            }
                                        })}
                                    </div>
                                    <p className="card-text"> Poziom: {cValue.difficulty}</p>
                                    <p>id={cValue.id}</p>
                                    <a href="#" className="btn btn-lg">Kup dostęp</a>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    );
}

export default TrainingGroupGetAll;