def upgrade():
    # Comando para criar a tabela `carteira_saldo`
    op.create_table(
        'carteira_saldo',
        sa.Column('id_saldo', sa.Integer(), nullable=False),
        sa.Column('carteira_id', sa.Integer(), nullable=False),
        sa.Column('cripto_id', sa.Integer(), nullable=False),
        sa.Column('saldo', sa.Float(), nullable=False, default=0.0),
        sa.ForeignKeyConstraint(['carteira_id'], ['carteira.id_carteira']),
        sa.ForeignKeyConstraint(['cripto_id'], ['cripto.id_cripto']),
        sa.PrimaryKeyConstraint('id_saldo')
    )
