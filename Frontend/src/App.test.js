import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders search button', () => {
    render(<App />);
    const searchButton = screen.getByText(/Поиск/i);
    expect(searchButton).toBeInTheDocument();
});

test('search input works', () => {
    render(<App />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Кафе' } });
    expect(input.value).toBe('Кафе');
});