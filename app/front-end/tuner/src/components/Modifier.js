import { useState, useRef } from 'react';

const Modifier = (props) => {
  const { settings } = props;

  const [AR, setAR] = useState(settings.ar)
  const [HP, setHP] = useState(settings.hp)
  const [CS, setCS] = useState(settings.cs)
  const [OD, setOD] = useState(settings.od)
  const [rate, setRate] = useState(settings.rate)
  const [BPM, setBPM] = useState(settings.bpm)

  return (
    <div>{}</div>
  )
}

export default Modifier;