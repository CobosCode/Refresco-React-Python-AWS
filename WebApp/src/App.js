import React, { useState } from 'react';
import Item from './Item';

function App() {
  const [items, setItems] = useState([]);
  const [text, setText] = useState('');

  function handleChange(event) {
    setText(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (!text.length) {
      return;
    }
    const newItem = {
      text: text,
      id: Date.now()
    };
    setItems(items.concat(newItem));
    setText('');
  }

  return (
    <div>
      <h1>Listado de Cosas</h1>
      <form onSubmit={handleSubmit}>
        <input onChange={handleChange} value={text} />
        <button>Añadir</button>
      </form>
      <ul>
        {items.map(item => (
          <Item key={item.id} item={item} />
        ))}
      </ul>
    </div>
  );
}

export default App;
