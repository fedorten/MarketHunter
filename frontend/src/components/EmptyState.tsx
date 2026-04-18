type Props = {
  title: string
  text: string
}

export function EmptyState({ title, text }: Props) {
  return (
    <div className="empty-state">
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
  )
}
