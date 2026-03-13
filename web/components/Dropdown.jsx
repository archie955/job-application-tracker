const DropDown = ({ status, setStatus, datatype }) => {
    const handleChange = (e) => {
        setStatus(e.target.value)
    }
    const keys = Object.keys(datatype)
    return (
        <select name="dropdown" value={status} onChange={handleChange}>
            {keys.map(key => 
                <option key={key} value={datatype[key]}>{key}</option>
            )}
        </select>
    )
}

export default DropDown