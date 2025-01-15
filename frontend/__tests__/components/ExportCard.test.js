import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { ExportCard } from '../../components/ExportCard';

describe('ExportCard Component', () => {
  const mockProps = {
    title: 'Export to Excel',
    description: 'Export data to Excel format',
    icon: () => <div>Icon</div>,
    onExport: jest.fn(),
    isLoading: false
  };

  test('renders with correct title and description', () => {
    const { getByText } = render(<ExportCard {...mockProps} />);
    expect(getByText(mockProps.title)).toBeInTheDocument();
    expect(getByText(mockProps.description)).toBeInTheDocument();
  });

  test('calls onExport when button is clicked', () => {
    const { getByRole } = render(<ExportCard {...mockProps} />);
    fireEvent.click(getByRole('button'));
    expect(mockProps.onExport).toHaveBeenCalled();
  });
});
